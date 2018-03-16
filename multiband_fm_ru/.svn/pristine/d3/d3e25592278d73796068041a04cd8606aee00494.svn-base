function fm_realign_unwarp(strFileNii,strFileVDM,strFileRefNii)
% EXAMPLE
% fm_realign_unwarp('tprun_01.nii','vdm5_fpm0000.img','run_01.nii')

[strNiiPath,strNiiName,strNiiExt] = fileparts(strFileNii);
%[strRefPath,strRefName,strRefExt] = fileparts(strFileRefNii);

% Take 10th volume of the ref image, append to input nii
imgRef = read_nii_img(strFileRefNii);
imgRef = imgRef(10,:);

[imgNii,hdrNii] = read_nii_img(strFileNii);

imgTmp = [imgRef;imgNii];
hdrTmp = hdrNii;
hdrTmp.dim(5) = hdrNii.dim(5)+1;
strFileTmp = fullfile(strNiiPath,['tmpru_' strNiiName strNiiExt]);
write_nii(strFileTmp,imgTmp,hdrTmp,0)

% strPat = sprintf('^%s$',[strNiiName strNiiExt]);
strPat = sprintf('^%s$',['tmpru_' strNiiName strNiiExt]);
chrScans = spm_select('ExtFPList',strNiiPath,strPat);
casScans = strtrim(mat2cell(chrScans,ones(size(chrScans,1),1),size(chrScans,2)));


matlabbatch{1}.spm.spatial.realignunwarp.data.scans = casScans;
matlabbatch{1}.spm.spatial.realignunwarp.data.pmscan = {sprintf('%s,1',strFileVDM)};
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.quality = 0.9;
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.sep = 4;
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.fwhm = 5;
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.rtm = 0;
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.einterp = 2;
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.ewrap = [0 0 0];
matlabbatch{1}.spm.spatial.realignunwarp.eoptions.weight = '';
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.basfcn = [12 12];
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.regorder = 1;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.lambda = 100000;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.jm = 0;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.fot = [4 5];
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.sot = [];
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.uwfwhm = 4;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.rem = 1;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.noi = 5;
matlabbatch{1}.spm.spatial.realignunwarp.uweoptions.expround = 'Average';
matlabbatch{1}.spm.spatial.realignunwarp.uwroptions.uwwhich = [2 1];
matlabbatch{1}.spm.spatial.realignunwarp.uwroptions.rinterp = 4;
matlabbatch{1}.spm.spatial.realignunwarp.uwroptions.wrap = [0 0 0];
matlabbatch{1}.spm.spatial.realignunwarp.uwroptions.mask = 1;
matlabbatch{1}.spm.spatial.realignunwarp.uwroptions.prefix = 'u';

spm('defaults', 'FMRI');
spm_jobman('run', matlabbatch);

% Rename the tmp files
!for i in $(ls *tmpru_*); do mv $i ${i/tmpru_/};done

% Strip off first vol
strFileOut = fullfile(strNiiPath,['u' strNiiName strNiiExt]);
[img,hdr] = read_nii_img(strFileOut);
imgNew = img(2:end,:);
hdr.dim(5) = hdr.dim(5)-1;
write_nii(strFileOut,imgNew,hdr,0)
